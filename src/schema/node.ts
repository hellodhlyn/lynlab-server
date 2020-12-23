import { fromGlobalId } from 'graphql-relay';
import { GraphQLInterfaceType, GraphQLID, GraphQLNonNull } from 'graphql/type';
import { getRepository } from 'typeorm';
import { postType, postTypeName } from './post';
import { Post } from '../models/post.model';

export const nodeInterface = new GraphQLInterfaceType({
  name: 'Node',
  fields: {
    id: { type: new GraphQLNonNull(GraphQLID) },
  },
  resolveType(src: any) {
    if (src instanceof Post) return postType;
    return null;
  },
});

export class NodeResolver {
  async node(_: undefined, args: { id: string }): Promise<any> {
    const { type, id } = fromGlobalId(args.id);
    switch (type) {
      case postTypeName:
        return getRepository<Post>('Post').findOne({ id: parseInt(id, 10) });
      default:
        throw new Error('invalid node id');
    }
  }
}
