import { GraphQLSchema } from 'graphql';
import Koa from 'koa';
import mount from 'koa-mount';
import graphqlHTTP from 'koa-graphql';
import { buildQueryType } from './schema/query';

export function createServer(): Koa {
  const schema = new GraphQLSchema({ query: buildQueryType() });

  const app = new Koa();
  app.use(mount('/graphql', graphqlHTTP({ schema, graphiql: true })));

  return app;
}
