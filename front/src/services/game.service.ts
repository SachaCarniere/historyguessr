import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {BaseService} from './service';
import {BehaviorSubject} from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class GameService extends BaseService {

  private url;
  public currentGameId$: BehaviorSubject<number> = new BehaviorSubject<number>(0);

  constructor(private http: HttpClient) {
    super();
    this.url = super.getBaseUrl() + 'game/';
  }

  public newGame(): void {
    this.http.post(this.url, '')
      .subscribe(response => {
        this.currentGameId$.next(response['id']);
      });
  }
}
