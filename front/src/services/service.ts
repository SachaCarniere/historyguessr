export class BaseService{
  protected baseUrl = 'http://localhost:8000/';

  protected getBaseUrl(): string {
    return this.baseUrl;
  }
}
