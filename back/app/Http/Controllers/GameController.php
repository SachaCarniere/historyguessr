<?php

namespace App\Http\Controllers;

use App\Game;
use App\GuessResult;
use App\Image;
use App\Round;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\Routing\ResponseFactory;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Ramsey\Uuid\Uuid;

class GameController extends Controller
{
    public function create(Request $request)
    {
        $game = new Game();
        $game->uuid = Uuid::uuid4();
        if ($request->input('category') != 'Tout') {
            $game->category = $request->input('category');
        }
        $game->save();

        if ($game->category == null) {
            $images_random = Image::orderByRaw('RAND()')->take(10)->get();
        } else {
            $images_random = Image::where('category', $game->category)->orderByRaw('RAND()')->take(10)->get();
        }
        foreach ($images_random as $key=>$value) {
            $round = new Round();
            $round->index = $key + 1;
            $round->year = $value->year;
            $game->rounds()->save($round);
        }

        return $game;
    }

    public function createWithUUID(Request $request, string $uuid) {
        $shared_game = Game::where('uuid', $uuid)->first();

        $game = new Game();
        $game->uuid = $shared_game->uuid;
        $game->category = $shared_game->category;
        $game->save();

        foreach ($shared_game->rounds()->get() as $key=>$value) {
            $round = new Round();
            $round->index = $value->index;
            $round->year = $value->year;
            $game->rounds()->save($round);
        }

        return $game;
    }

    public function answer(Request $request, int $game_id, int $round) {
        $game = Game::find($game_id);
        if(!$game) {
            return response('Game ID unknown', 404);
        }
        $round = $game->rounds()->where('index', $round)->first();
        if ($round->year_answered != null) {
            return response('Round already answered', 403);
        }

        $round->year_answered = $request->input("guess");
        $round->save();



        return new GuessResult((int) $request->input("guess"), $round->year, $round->id, $round->amount_unlocked);
    }
}
