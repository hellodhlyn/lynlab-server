import {
  Column, CreateDateColumn, Entity, ManyToOne, PrimaryGeneratedColumn, UpdateDateColumn,
} from 'typeorm';
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

  @ManyToOne(() => Post, (post) => post.blobs)
  post: Promise<Post>;

  @Column()
  content: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
