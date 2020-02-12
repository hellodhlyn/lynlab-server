'use strict';

const { sanitizeEntity } = require('strapi-utils');

async function findSnippets(ctx) {
  const { user } = ctx.state;
  if (!user || !user.confirmed || (user.role.type !== 'authenticated')) {
    ctx.query = { ...ctx.query, status: 'published' };
  }

  let entities;
  if (ctx.query._q) {
    entities = await strapi.services.snippet.search(ctx.query);
  } else {
    entities = await strapi.services.snippet.find(ctx.query);
  }

  return entities;
}

module.exports = {
  async find(ctx) {
    const entities = await findSnippets(ctx);
    return entities.map(entity => sanitizeEntity(entity, { model: strapi.models.snippet }));
  },

  async findOne(ctx) {
    const entities = await findSnippets(ctx);
    const entity = entities.length > 0 ? entities[0] : null;
    return sanitizeEntity(entity, { model: strapi.models.snippet });
  },

  async findOneRaw(ctx) {
    const entities = await findSnippets(ctx);
    if (entities.length > 0) {
      return entities[0].body;
    }
  },
};
