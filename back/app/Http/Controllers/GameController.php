<?php


namespace App\Http\Controllers;

use App\Game;
use Illuminate\Http\Request;

class GameController extends Controller
{
    public function createGame(Request $request) {

        $game = new Game();
        $game->year = 1998;
        $game->save();

        return $game;
    }
}
