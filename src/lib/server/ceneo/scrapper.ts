import * as cheerio from "cheerio"

export class Scrapper {
  private page: cheerio.CheerioAPI | null = null;

  async query(url: string): Promise<boolean> {
    const response = await fetch(url);

    if (!response.ok) {
      return false;
    }
  
    const content = await response.text();

    this.page = cheerio.load(content)

    return true;
  }
}