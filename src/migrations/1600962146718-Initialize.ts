import { MigrationInterface, QueryRunner, Table } from 'typeorm';

export class Initialize1600962146718 implements MigrationInterface {

  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.createTable(new Table({
      name: 'posts',
      columns: [
        { name: 'id', type: 'bigint', isPrimary: true, isGenerated: true },
        { name: 'title', type: 'text' },
        { name: 'description', type: 'text', isNullable: true },
        { name: 'thumbnail_url', type: 'text', isNullable: true },
        { name: 'series_id', type: 'bigint', isNullable: true },
        { name: 'created_at', type: 'timestamp with time zone', default: 'now()' },
        { name: 'updated_at', type: 'timestamp with time zone', default: 'now()' },
      ],
    }));

    await queryRunner.createTable(new Table({
      name: 'post_blobs',
      columns: [
        { name: 'id', type: 'bigint', isPrimary: true, isGenerated: true },
        { name: 'uuid', type: 'varchar', length: '36' },
        { name: 'post_id', type: 'bigint' },
        { name: 'order', type: 'int' },
        { name: 'blob_type', type: 'varchar', length: '40' },
        { name: 'content', type: 'text' },
        { name: 'created_at', type: 'timestamp with time zone', default: 'now()' },
        { name: 'updated_at', type: 'timestamp with time zone', default: 'now()' },
      ],
      indices: [
        { columnNames: ['uuid'], isUnique: true },
        { columnNames: ['post_id', 'order'], isUnique: true },
      ],
    }));

    await queryRunner.createTable(new Table({
      name: 'post_tags',
      columns: [
        { name: 'id', type: 'bigint', isPrimary: true, isGenerated: true },
        { name: 'name', type: 'varchar', length: '40' },
        { name: 'slug', type: 'varchar', length: '40' },
        { name: 'created_at', type: 'timestamp with time zone', default: 'now()' },
        { name: 'updated_at', type: 'timestamp with time zone', default: 'now()' },
      ],
      indices: [
        { columnNames: ['slug'], isUnique: true },
        { columnNames: ['name'], isUnique: true },
      ],
    }));

    await queryRunner.createTable(new Table({
      name: 'post_tag_relations',
      columns: [
        { name: 'post_id', type: 'bigint' },
        { name: 'tag_id', type: 'bigint' },
      ],
      indices: [
        { columnNames: ['post_id'] },
        { columnNames: ['tag_id'] },
      ],
    }));

    await queryRunner.createTable(new Table({
      name: 'post_series',
      columns: [
        { name: 'id', type: 'bigint', isPrimary: true, isGenerated: true },
        { name: 'name', type: 'text' },
        { name: 'created_at', type: 'timestamp with time zone', default: 'now()' },
        { name: 'updated_at', type: 'timestamp with time zone', default: 'now()' },
      ],
    }));
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropTable('post_series');
    await queryRunner.dropTable('post_tag_relations');
    await queryRunner.dropTable('post_tags');
    await queryRunner.dropTable('post_blobs');
    await queryRunner.dropTable('posts');
  }

}
