import { GraphQLObjectType } from 'graphql';
import {
  GraphQLNonNull, GraphQLString, GraphQLInt, GraphQLEnumType,
} from 'graphql/type';
import { GraphQLDateTime } from 'graphql-iso-date';
import { postType } from './post';

export const postBlobTypeName = 'PostBlob';

export const blobTypeEnumType = new GraphQLEnumType({
  name: 'BlobType',
  values: {
    MARKDOWN: { value: 'MARKDOWN' },
  },
});

export const postBlobType: GraphQLObjectType = new GraphQLObjectType({
  name: postBlobTypeName,
  fields: () => ({
    uuid: { type: new GraphQLNonNull(GraphQLString) },
    order: { type: new GraphQLNonNull(GraphQLInt) },
    content: { type: new GraphQLNonNull(GraphQLString) },
    blobType: { type: new GraphQLNonNull(blobTypeEnumType) },
    post: { type: new GraphQLNonNull(postType) },
    createdAt: { type: new GraphQLNonNull(GraphQLDateTime) },
    updatedAt: { type: new GraphQLNonNull(GraphQLDateTime) },
  }),
});
