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
  private pathList: string[] = [];
  public currentGameId$: BehaviorSubject<number> = new BehaviorSubject<number>(0);
  public currentGameUUID$: BehaviorSubject<string> = new BehaviorSubject<string>('');
  public currentRound$: BehaviorSubject<number> = new BehaviorSubject<number>(1);
  public images$: BehaviorSubject<string[]> = new BehaviorSubject(this.pathList);
  public score$: BehaviorSubject<number> = new BehaviorSubject<number>(0);
  public maxImg$: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

  constructor(private http: HttpClient) {
    super();
    this.url = super.getBaseUrl() + 'game/';
  }

  public newGame(): Promise<number> {
    return new Promise<number>((resolve, reject) => {
      this.http.post(this.url, '')
        .subscribe(res => {
          this.currentGameId$.next(res['id']);
          this.currentGameUUID$.next(res['uuid']);
          resolve(res['id']);
        });
    });
  }

  public newGameWithUUID(uuid: string): Promise<number> {
    return new Promise<number>((resolve, reject) => {
      this.http.post(this.url + uuid, {uuid: uuid})
        .subscribe(res => {
          this.currentGameId$.next(res['id']);
          this.currentGameUUID$.next(res['uuid']);
          resolve(res['id']);
        });
    });
  }

  public getScore(guess: number): Promise<GuessResult> {
    return new Promise<GuessResult>((resolve, reject) => {
      this.http.post(this.url + 'answer/' + this.currentGameId$.getValue() + '/' + this.currentRound$.getValue(), {guess: guess})
        .subscribe(res =>
          resolve(new GuessResult(res['guess'], res['actualYear'], res['score'], res['images'], res['event_names'], res['captions'])));
    });
  }

  public getNextImage(): Promise<string>{
    return new Promise<string>((resolve, reject) => {
      this.http.get(this.url + 'randomImage/' + this.currentGameId$.getValue() + '/' + this.currentRound$.getValue())
        .subscribe(res =>  {
          this.pathList = [];
          this.images$.next(this.pathList);
          this.pathList.push(res['path']);
          this.images$.next(this.pathList);
          resolve(res['path']);
        }, error => {
          this.maxImg$.next(true);
        });
    });
  }

  public getAdditionnalImage(): Promise<string>{
    return new Promise<string>((resolve, reject) => {
      this.http.get(this.url + 'randomImage/' + this.currentGameId$.getValue() + '/' + this.currentRound$.getValue())
        .subscribe(res =>  {
          this.pathList.push(res['path']);
          this.images$.next(this.pathList);
          resolve(res['path']);
        }, error => {
          this.maxImg$.next(true);
        });
    });
  }
}
