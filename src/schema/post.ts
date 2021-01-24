import { GraphQLInputObjectType, GraphQLObjectType } from 'graphql';
import {
  GraphQLBoolean, GraphQLInt, GraphQLList, GraphQLNonNull, GraphQLString,
} from 'graphql/type';
import {
  Connection, connectionArgs, ConnectionArguments, connectionDefinitions, cursorToOffset, globalIdField, offsetToCursor,
} from 'graphql-relay';
import { GraphQLDateTime } from 'graphql-iso-date';
import {
  FindConditions, getManager, getRepository, In, LessThan, MoreThan, Not,
} from 'typeorm';
import { nodeInterface } from './node';
import { createPostBlobInputType, postBlobType } from './post-blob';
import { postSeriesType } from './post-series';
import { postTagType } from './post-tag';
import { Post } from '../models/post.model';
import { BlobType, PostBlob } from '../models/post-blob.model';

async function findPostConnection(where: FindConditions<Post>[], args: ConnectionArguments): Promise<Connection<Post>> {
  const repo = getRepository<Post>('Post');

  let whereQuery = where;
  if (args.after) {
    whereQuery = where.map((each) => ({ ...each, id: LessThan(cursorToOffset(args.after)) }));
  } else if (args.before) {
    whereQuery = where.map((each) => ({ ...each, id: MoreThan(cursorToOffset(args.before)) }));
  }

  whereQuery = whereQuery.map((each) => ({ ...each, isPublic: true }));

  const order: { id: 'ASC' | 'DESC' } = { id: (args.last ? 'ASC' : 'DESC') };
  const take = args.last || args.first || 20;
  const result = await repo.find({ where: whereQuery, order, take });
  result.sort((a, b) => b.id - a.id);

  return {
    edges: result.map((node) => ({ cursor: offsetToCursor(node.id), node })),
    pageInfo: result.length === 0 ? {
      startCursor: null,
      endCursor: null,
      hasNextPage: false,
      hasPreviousPage: false,
    } : {
      startCursor: offsetToCursor(result[0].id),
      endCursor: offsetToCursor(result[result.length - 1].id),
      hasPreviousPage: await repo.count({ id: MoreThan(result[0].id) }) > 0,
      hasNextPage: await repo.count({ id: LessThan(result[result.length - 1].id) }) > 0,
    },
  };
}

export const postTypeName = 'Post';

export const postType: GraphQLObjectType = new GraphQLObjectType({
  name: postTypeName,
  interfaces: [nodeInterface],
  fields: () => ({
    id: globalIdField(postTypeName, (src: Post) => src.id.toString()),
    postId: { type: new GraphQLNonNull(GraphQLInt), resolve: (post) => post.id },
    title: { type: new GraphQLNonNull(GraphQLString) },
    description: { type: GraphQLString },
    thumbnailUrl: { type: GraphQLString },
    isPublic: { type: new GraphQLNonNull(GraphQLBoolean) },
    series: { type: postSeriesType },
    tags: { type: new GraphQLList(new GraphQLNonNull(postTagType)) },
    blobs: {
      type: new GraphQLList(new GraphQLNonNull(postBlobType)),
      resolve: async (post) => {
        const repo = getRepository<PostBlob>('PostBlob');
        return repo.find({ where: { postId: post.id }, order: { order: 'ASC' } });
      },
    },
    relatedPosts: {
      // eslint-disable-next-line no-use-before-define
      type: postConnectionType,
      args: connectionArgs,
      resolve: async (post: Post, args: ConnectionArguments): Promise<Connection<Post>> => {
        const where: FindConditions<Post>[] = [];

        const series = await post.series;
        if (series) {
          where.push({ seriesId: series.id, id: Not(post.id) });
        }

        const tags = await post.tags;
        if (tags.length > 0) {
          const postIds = (await Promise.all(tags.map((tag) => tag.posts)))
            .reduce((prev, cur) => prev.concat(cur))
            .map((p) => p.id)
            .filter((val, idx, self) => (self.indexOf(val) === idx) && (val !== post.id));
          if (postIds.length > 0) {
            where.push({ id: In(postIds) });
          }
        }

        if (where.length === 0) {
          return { edges: [], pageInfo: {} };
        }
        return findPostConnection(where, args);
      },
    },
    createdAt: { type: new GraphQLNonNull(GraphQLDateTime) },
    updatedAt: { type: new GraphQLNonNull(GraphQLDateTime) },
  }),
});

export const postConnectionType: GraphQLObjectType = connectionDefinitions({ nodeType: postType }).connectionType;

export const createPostInputType = new GraphQLInputObjectType({
  name: 'CreatePostInput',
  fields: () => ({
    title: { type: new GraphQLNonNull(GraphQLString) },
    description: { type: new GraphQLNonNull(GraphQLString) },
    thumbnailUrl: { type: GraphQLString },
    isPublic: { type: new GraphQLNonNull(GraphQLBoolean) },
    seriesId: { type: GraphQLInt },
    blobs: { type: new GraphQLList(new GraphQLNonNull(createPostBlobInputType)) },
  }),
});

export type CreatePostInputType = {
  title: string;
  description: string;
  thumbnailUrl: string;
  isPublic: boolean;
  seriesId: number;
  blobs: {
    blobType: string;
    content: string;
  }[];
}

export class PostResolver {
  async posts(_: undefined, args: ConnectionArguments): Promise<Connection<Post>> {
    return findPostConnection([{}], args);
  }

  async post(_: undefined, args: { postId: number }): Promise<Post> {
    const repo = getRepository<Post>('Post');
    return repo.findOne({ id: args.postId, isPublic: true });
  }

  async createPost(_: undefined, args: { input: CreatePostInputType }): Promise<Post> {
    const { input } = args;
    const post = new Post();
    post.title = input.title;
    post.description = input.description;
    post.thumbnailUrl = input.thumbnailUrl || null;
    post.isPublic = input.isPublic || false;
    post.seriesId = input.seriesId || null;

    await getManager().transaction(async (em) => {
      await em.save(post);
      await Promise.all(input.blobs.map((blobInput, idx) => {
        const blob = new PostBlob();
        blob.blobType = BlobType.MARKDOWN;
        blob.content = blobInput.content;
        blob.postId = post.id;
        blob.order = idx;
        return em.save(blob);
      }));
    });

    return post;
  }
}
