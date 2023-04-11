import { PrismaClient, type Product } from '@prisma/client';
import type { CeneoProduct } from './ceneoProduct';

const prisma = new PrismaClient();

await prisma.$connect();

const formatProductData = (product: CeneoProduct): Omit<Product, 'id'> => {
  return {
    ceneoProductId: product.id,
    name: product.name,
    partialExtraction: product.partialExtraction,
    overview: {
      reviewsCount: product.reviewsCount,
      prosCount: product.prosCount,
      consCount: product.consCount,
      averageScore: product.averageScore
    },
    reviews: product.reviews.map((review) => ({
      ceneoReviewId: review.id,
      author: review.author,
      recommendation: review.recommendation,
      score: review.score,
      verified: review.verified,
      published: review.published,
      bought: review.bought,
      votesYes: review.votesYes,
      votesNo: review.votesNo,
      text: review.text,
      pros: review.pros,
      cons: review.cons
    }))
  };
};

export const insertProduct = async (product: CeneoProduct) => {
  return await prisma.product.create({
    data: formatProductData(product)
  });
};

export const updateProduct = async (ceneoProductId: string, product: CeneoProduct) => {
  return await prisma.product.update({
    where: {
      ceneoProductId: ceneoProductId
    },
    data: formatProductData(product)
  });
};

export const getProductById = async (ceneoProductId: string) => {
  return await prisma.product.findUnique({
    where: {
      ceneoProductId
    }
  });
};

export const getProductsOverview = async () => {
  return await prisma.product.findMany({
    select: {
      ceneoProductId: true,
      name: true,
      overview: true
    }
  });
};
