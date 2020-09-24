import { GraphQLObjectType } from 'graphql';
import { GraphQLNonNull, GraphQLList, GraphQLString } from 'graphql/type';
import { postType } from './post';

export const postTagTypeName = 'PostTag';

export const postTagType: GraphQLObjectType = new GraphQLObjectType({
  name: postTagTypeName,
  fields: () => ({
    name: { type: new GraphQLNonNull(GraphQLString) },
    posts: {
      type: new GraphQLList(new GraphQLNonNull(postType)),
    },
  }),
});
