import { Component, OnInit } from '@angular/core';
import {GameService} from '../../services/game.service';
import {Router} from '@angular/router';
import {environment} from '../../environments/environment';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  score: number;
  env = environment;
  uuid: string;

  constructor(private gameService: GameService, private router: Router){
    this.gameService.score$.subscribe(score => this.score = score);
    this.gameService.currentGameUUID$.subscribe(uuid => this.uuid = uuid);
  }

  ngOnInit(): void {
  }

  public play(): void {
    this.gameService.score$.next(0);
    this.gameService.currentRound$.next(1);
    this.gameService.images$.next([]);

    this.gameService.newGame().then( () => this.router.navigate(['./game/']));
  }
}
