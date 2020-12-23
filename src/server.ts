import cors from '@koa/cors';
import { GraphQLSchema } from 'graphql';
import Koa from 'koa';
import mount from 'koa-mount';
import graphqlHTTP from 'koa-graphql';
import { buildQueryType } from './schema/query';

const allowedOrigins = process.env.CORS_ALLOWED_ORIGINS?.split(',');

export function createServer(): Koa {
  const schema = new GraphQLSchema({ query: buildQueryType() });

  const app = new Koa();
  app.use(cors({
    origin: (ctx: Koa.Context) => {
      const { origin } = ctx.headers;
      return allowedOrigins?.includes(origin) ? origin : false;
    },
  }));

  app.use(mount('/ping', (ctx: Koa.Context) => { ctx.body = 'pong'; }));
  app.use(mount('/graphql', graphqlHTTP({ schema, graphiql: true })));

  return app;
}
