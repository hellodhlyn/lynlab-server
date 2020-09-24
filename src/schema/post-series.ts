import { GraphQLObjectType } from 'graphql';
import { GraphQLNonNull, GraphQLList, GraphQLString } from 'graphql/type';
import { postType } from './post';

export const postSeriesTypeName = 'PostSeries';

export const postSeriesType: GraphQLObjectType = new GraphQLObjectType({
  name: postSeriesTypeName,
  fields: () => ({
    name: { type: new GraphQLNonNull(GraphQLString) },
    posts: { type: new GraphQLList(new GraphQLNonNull(postType)) },
  }),
});
