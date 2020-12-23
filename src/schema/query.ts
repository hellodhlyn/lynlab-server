import { GraphQLObjectType } from 'graphql';
import { GraphQLNonNull, GraphQLID, GraphQLInt } from 'graphql/type';
import { connectionArgs } from 'graphql-relay';
import { postConnectionType, PostResolver, postType } from './post';

// `nodeInterface` should be loaded at last to avoid cyclic dependency.
import { nodeInterface, NodeResolver } from './node';

export function buildQueryType(): GraphQLObjectType {
  const nodeResolver = new NodeResolver();
  const postResolver = new PostResolver();

  return new GraphQLObjectType({
    name: 'Query',
    fields: () => ({
      node: {
        type: nodeInterface,
        args: { id: { type: new GraphQLNonNull(GraphQLID) } },
        resolve: (_, args: { id: string }) => nodeResolver.node(_, args),
      },
      posts: {
        type: new GraphQLNonNull(postConnectionType),
        args: connectionArgs,
        resolve: (_, args) => postResolver.posts(_, args),
      },
      post: {
        type: new GraphQLNonNull(postType),
        args: { postId: { type: new GraphQLNonNull(GraphQLInt) } },
        resolve: (_, args: { postId: number }) => postResolver.post(_, args),
      },
    }),
  });
}
