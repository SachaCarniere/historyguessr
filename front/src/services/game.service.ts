import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {BaseService} from './service';
import {BehaviorSubject} from 'rxjs';
import {GuessResult} from '../types/GuessResult';

@Injectable({
  providedIn: 'root'
})

export class GameService extends BaseService {

  private url;
  private pathList: string[] = [];
  private categories: string[] = [];
  public currentGameId$: BehaviorSubject<number> = new BehaviorSubject<number>(0);
  public currentGameUUID$: BehaviorSubject<string> = new BehaviorSubject<string>('');
  public currentRound$: BehaviorSubject<number> = new BehaviorSubject<number>(1);
  public images$: BehaviorSubject<string[]> = new BehaviorSubject(this.pathList);
  public score$: BehaviorSubject<number> = new BehaviorSubject<number>(0);
  public maxImg$: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public categories$: BehaviorSubject<string[]> = new BehaviorSubject<string[]>(this.categories);

  constructor(private http: HttpClient) {
    super();
    this.url = super.getBaseUrl() + 'game/';
  }

  public newGame(category: string): Promise<number> {
    let body = new HttpParams();
    body = body.set('category', category);

    return new Promise<number>((resolve, reject) => {
      this.http.post(this.url, body)
        .subscribe(res => {
          this.currentGameId$.next(res['id']);
          this.currentGameUUID$.next(res['uuid']);
          resolve(res['id']);
        });
    });
  }

  public newGameWithUUID(uuid: string, category: string): Promise<number> {
    let body = new HttpParams();
    body = body.set('category', category);

    return new Promise<number>((resolve, reject) => {
      this.http.post(this.url + uuid, body)
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

  public getCategories(): Promise<string[]>{
    return new Promise<string[]>((resolve, reject) => {
      this.http.get(super.getBaseUrl() + 'getCategories')
        .subscribe((res: any[]) =>  {
          // Flush
          this.categories = [];
          this.categories$.next(this.categories);
          // Default value
          this.categories.push('Tout');
          // Categories from back
          for (let i = 0; i < res.length; i++) {
            this.categories.push(res[i]);
          }
          this.categories$.next(this.categories);
          }, error => {
          console.log(error);
        });
    });
  }
}
