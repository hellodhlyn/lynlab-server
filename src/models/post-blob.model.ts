import {
  BeforeInsert,
  Column, CreateDateColumn, Entity, ManyToOne, PrimaryGeneratedColumn, UpdateDateColumn,
} from 'typeorm';
import { v4 as uuidv4 } from 'uuid';
import { Post } from './post.model';

export enum BlobType {
  MARKDOWN = 'MARKDOWN',
}

@Entity('post_blobs')
export class PostBlob {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  uuid: string;

  @Column()
  order: number;

  @Column()
  blobType: BlobType;

  @Column()
  postId: number;

  @ManyToOne(() => Post, (post) => post.blobs)
  post: Promise<Post>;

  @Column()
  content: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  @BeforeInsert()
  private beforeInsert() {
    this.uuid = uuidv4();
  }
}
