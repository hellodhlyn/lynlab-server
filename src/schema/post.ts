import { GraphQLObjectType } from 'graphql';
import { GraphQLString, GraphQLNonNull, GraphQLList } from 'graphql/type';
import {
  Connection, ConnectionArguments, connectionDefinitions, cursorToOffset, globalIdField, offsetToCursor,
} from 'graphql-relay';
import { GraphQLDateTime } from 'graphql-iso-date';
import {
  FindConditions, getRepository, LessThan, MoreThan,
} from 'typeorm';
import { nodeInterface } from './node';
import { postBlobType } from './post-blob';
import { postSeriesType } from './post-series';
import { postTagType } from './post-tag';
import { Post } from '../models/post.model';

export const postTypeName = 'Post';

export const postType: GraphQLObjectType = new GraphQLObjectType({
  name: postTypeName,
  interfaces: [nodeInterface],
  fields: () => ({
    id: globalIdField(postTypeName, (src: Post) => src.id.toString()),
    title: { type: new GraphQLNonNull(GraphQLString) },
    description: { type: GraphQLString },
    thumbnailUrl: { type: GraphQLString },
    series: { type: postSeriesType },
    tags: { type: new GraphQLList(new GraphQLNonNull(postTagType)) },
    blobs: { type: new GraphQLList(new GraphQLNonNull(postBlobType)) },
    createdAt: { type: new GraphQLNonNull(GraphQLDateTime) },
    updatedAt: { type: new GraphQLNonNull(GraphQLDateTime) },
  }),
});

export const postConnectionType: GraphQLObjectType = connectionDefinitions({ nodeType: postType }).connectionType;

export class PostResolver {
  async posts(_: undefined, args: ConnectionArguments): Promise<Connection<Post>> {
    const repo = getRepository<Post>('Post');

    const where: FindConditions<Post> = {};
    if (args.after) {
      where.id = LessThan(cursorToOffset(args.after));
    } else if (args.before) {
      where.id = MoreThan(cursorToOffset(args.before));
    }

    const order: { id: 'ASC' | 'DESC' } = { id: (args.last ? 'ASC' : 'DESC') };
    const take = args.last || args.first || 20;
    const result = await repo.find({ where, order, take });
    result.sort((r) => r.id);

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
}
