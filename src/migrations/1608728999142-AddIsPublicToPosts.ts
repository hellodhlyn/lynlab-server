import { MigrationInterface, QueryRunner, TableColumn, TableIndex } from 'typeorm';

export class AddIsPublicToPosts1608728999142 implements MigrationInterface {

  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.addColumn('posts', new TableColumn({ name: 'is_public', type: 'boolean', default: 'false' }));
    await queryRunner.createIndex('posts', new TableIndex({ columnNames: ['is_public', 'id'] }));
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropIndex('posts', new TableIndex({ columnNames: ['is_public', 'id'] }));
    await queryRunner.dropColumn('posts', 'is_public');
  }

}
