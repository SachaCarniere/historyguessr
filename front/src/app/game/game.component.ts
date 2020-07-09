import { Component, OnInit } from '@angular/core';
import {GameService} from '../../services/game.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit {

  images: string;
  yearGuess: number;
  score: number;
  currentRound: number;

  constructor(private gameService: GameService, private router: Router){
    this.gameService.getNextImage().then(path => this.images = path);
    console.log(this.images);
    this.score = 0;
    this.gameService.currentRound$.subscribe(round => this.currentRound = round);
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    this.gameService.getScore(this.yearGuess).then(guessResult => this.score += guessResult.score);
    this.gameService.getNextImage().then(path => this.images = path);
    if (this.currentRound < 10) {
      this.gameService.currentRound$.next(this.currentRound + 1);
    } else {
      this.router.navigate(['./result/']);
    }
  }
}
