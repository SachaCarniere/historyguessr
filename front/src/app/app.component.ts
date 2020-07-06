import { Component } from '@angular/core';
import {GameService} from '../services/game.service';
import {AppRoutingModule} from './app-routing.module';
import {Routes, RouterModule, Router} from '@angular/router';
import {GameComponent} from './game/game.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'HistoryGuessr';

  constructor(private gameService: GameService, private router: Router) {
  }



  public play(): void {
    this.gameService.currentGameId$.subscribe(id => this.router.navigate(['./game/'])); // Redirect quand l'ID est update
    this.gameService.newGame();
  }
}
