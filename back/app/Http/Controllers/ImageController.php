<?php

namespace App\Http\Controllers;

use App\Game;
use App\Image;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\Routing\ResponseFactory;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class ImageController extends Controller
{
    /**
     * Get random picture with same year that game ID
     *
     * @param Request $request
     * @param int $id
     * @return Image|Application|ResponseFactory|Response
     */
    public function randomImage(Request $request, int $game_id, int $round)
    {
        $game = Game::find($game_id);
        if(!$game) {
            return response('Game ID unknown', 404);
        }

        $image = Image::where('year', $game->rounds()->where('index', $round)->first()->year)->orderByRaw('RAND()')->first();
        if(!$image) {
            return response('No image available', 404);
        }

        $image->path = env('APP_URL').":8000/storage/img/".$image->path;

        return $image;
    }
}
