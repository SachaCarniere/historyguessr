import { Component, OnInit } from '@angular/core';
import {GameService} from '../../services/game.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  score: number;

  constructor(private gameService: GameService, private router: Router){
    this.gameService.score$.subscribe(score => this.score = score);
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
