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