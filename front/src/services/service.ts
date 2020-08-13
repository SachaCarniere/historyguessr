import {environment} from '../environments/environment';

export class BaseService {
  protected baseUrl = environment.url_back;

  protected getBaseUrl(): string {
    return this.baseUrl;
  }
}
