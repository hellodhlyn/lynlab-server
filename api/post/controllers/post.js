'use strict';

const { sanitizeEntity } = require('strapi-utils');

async function findPosts(ctx) {
  const { user } = ctx.state;
  if (!user || !user.confirmed || (user.role.type !== 'authenticated')) {
    ctx.query = { ...ctx.query, status: 'published' };
  }

  let entities;
  if (ctx.query._q) {
    entities = await strapi.services.post.search(ctx.query);
  } else {
    entities = await strapi.services.post.find(ctx.query);
  }

  return entities;
}

module.exports = {
  async find(ctx) {
    const entities = await findPosts(ctx);
    return entities.map(entity => sanitizeEntity(entity, { model: strapi.models.post }));
  },

  async findOne(ctx) {
    const entities = await findPosts(ctx);
    const entity = entities.length > 0 ? entities[0] : null;
    return sanitizeEntity(entity, { model: strapi.models.post });
  },
};
