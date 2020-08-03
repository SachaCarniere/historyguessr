import { NgModule } from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {GameComponent} from './game/game.component';
import {HomeComponent} from './home/home.component';
import {ResultComponent} from './result/result.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'share/:uuid', component: HomeComponent },
  { path: 'game' , component: GameComponent },
  { path: 'result', component: ResultComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})



export class AppRoutingModule { }
