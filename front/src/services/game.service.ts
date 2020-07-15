import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {BaseService} from './service';
import {BehaviorSubject} from 'rxjs';
import {GuessResult} from '../types/GuessResult';

@Injectable({
  providedIn: 'root'
})

export class GameService extends BaseService {

  private url;
  public currentGameId$: BehaviorSubject<number> = new BehaviorSubject<number>(0);
  public currentRound$: BehaviorSubject<number> = new BehaviorSubject<number>(1);
  public currentImage$: BehaviorSubject<string> = new BehaviorSubject<string>('');

  constructor(private http: HttpClient) {
    super();
    this.url = super.getBaseUrl() + 'game/';
  }

  public newGame(): Promise<number> {
    return new Promise<number>((resolve, reject) => {
      this.http.post(this.url, '')
        .subscribe(res => {
          this.currentGameId$.next(res['id']);
          resolve(res['id']);
        });
    });
  }

  public getScore(guess: number): Promise<GuessResult> {
    return new Promise<GuessResult>((resolve, reject) => {
      this.http.post(this.url + 'answer/' + this.currentGameId$.getValue() + '/' + this.currentRound$.getValue(), {guess: guess})
        .subscribe(res =>
          resolve(new GuessResult(res['guess'], res['actualYear'], res['score'])));
    });
  }

  public getNextImage(): Promise<string>{
    return new Promise<string>((resolve, reject) => {
      this.http.get(this.url + 'randomImage/' + this.currentGameId$.getValue() + '/' + this.currentRound$.getValue())
        .subscribe(res =>  {
          this.currentImage$.next(res['path']);
          resolve(res['path']);
        });
    });
  }
}
