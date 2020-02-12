'use strict';

const { sanitizeEntity } = require('strapi-utils');

module.exports = {
  async find(ctx) {
    let entities;

    ctx.query = {
      ...ctx.query,
      status: 'published',
    };

    if (ctx.query._q) {
      entities = await strapi.services.post.search(ctx.query);
    } else {
      entities = await strapi.services.post.find(ctx.query);
    }

    return entities.map(entity =>
      sanitizeEntity(entity, { model: strapi.models.post })
    );
  },
};
