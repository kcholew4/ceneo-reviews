import { PrismaClient } from "@prisma/client";
import type { CeneoProduct } from "./ceneoProduct";

const prisma = new PrismaClient();

await prisma.$connect();

export const insertProduct = async (product: CeneoProduct) => {
  return await prisma.product.create({
    data: {
      ceneoProductId: product.id,
      name: product.name,
      partialExtraction: product.partialExtraction,
      reviews: product.reviews.map((review) => ({ ...review, ceneoReviewId: review.id }))
    }
  })
}

export const getProductById = async (ceneoProductId: string) => {
  return await prisma.product.findUnique({
    where: {
      ceneoProductId
    }
  })
}