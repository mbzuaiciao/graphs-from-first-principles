import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';

export const collections = {
  tutorials: defineCollection({
    loader: glob({ pattern: '*.md', base: '../tutorials' }),
  }),
};
