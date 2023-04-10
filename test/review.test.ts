import * as cheerio from 'cheerio';
import { describe, beforeAll, test, expect } from 'vitest';
import { SINGLE_REVIEW } from './data';
import { Review } from '../src/lib/ceneo/review';

describe('Review', () => {
  let review: Review;

  beforeAll(() => {
    const $ = cheerio.load(SINGLE_REVIEW, {}, false);
    review = new Review($('*'));
  });

  test('get id', () => {
    expect(review.id).toEqual('16890757');
  });

  test('get author', () => {
    expect(review.author).toEqual('tomaszloewnau');
  });

  test('get recommendation', () => {
    expect(review.recommendation).toEqual('Polecam');
  });

  test('get score', () => {
    expect(review.score).toEqual(5);
  });

  test('is verified', () => {
    expect(review.verified).toEqual(true);
  });

  test('get published date', () => {
    expect(review.published).toEqual(new Date('2022-12-16 11:15:13'));
  });

  test('get bought date', () => {
    expect(review.bought).toEqual(new Date('2022-12-09 16:29:50'));
  });

  test('get votes yes', () => {
    expect(review.votesYes).toEqual(0);
  });

  test('get votes no', () => {
    expect(review.votesNo).toEqual(0);
  });

  test('get text', () => {
    expect(review.text.slice(0, 19)).toEqual('Solidne wykończenie');
  });

  test('get pros', () => {
    expect(review.pros).toMatchObject(['głośność pracy', 'łatwość czyszczenia', 'wygoda używania']);
  });

  test('get cons', () => {
    expect(review.cons).toMatchObject([]);
  });
});
