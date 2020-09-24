import {
  Column, CreateDateColumn, Entity, JoinTable, ManyToMany, ManyToOne, OneToMany, PrimaryGeneratedColumn,
  UpdateDateColumn,
} from 'typeorm';
import { PostSeries } from './post-series.model';
import { PostTag } from './post-tag.model';
import { PostBlob } from './post-blob.model';

@Entity('posts')
export class Post {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  title: string;

  @Column()
  description: string;

  @Column()
  thumbnailUrl: string;

  @Column()
  seriesId: number;

  @ManyToOne(() => PostSeries)
  series: Promise<PostSeries>;

  @OneToMany(() => PostBlob, (blob) => blob.post)
  blobs: Promise<PostBlob>;

  @ManyToMany(() => PostTag, (tag) => tag.posts)
  @JoinTable({ name: 'post_tag_relations', joinColumn: { name: 'post_id' }, inverseJoinColumn: { name: 'tag_id' } })
  tags: Promise<PostTag[]>;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
