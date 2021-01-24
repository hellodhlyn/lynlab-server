import { GraphQLObjectType, GraphQLNonNull } from 'graphql';
import {
  CreatePostInputType, createPostInputType, PostResolver, postType,
} from './post';

export function buildMutationType(): GraphQLObjectType {
  const postResolver = new PostResolver();

  return new GraphQLObjectType({
    name: 'Mutation',
    fields: () => ({
      createPost: {
        type: postType,
        args: {
          input: {
            type: new GraphQLNonNull(createPostInputType),
          },
        },
        resolve: (_, args: { input: CreatePostInputType }) => postResolver.createPost(_, args),
      },
    }),
  });
}
