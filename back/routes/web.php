<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

/*Route::get('/', function () {
    return view('welcome');
});*/

Route::middleware('cors')->group(function () {
    Route::post('game', 'GameController@create');
    Route::post('game/{uuid}', 'GameController@createWithUUID');
    Route::post('game/answer/{game_id}/{round}', 'GameController@answer');

    Route::get('game/randomImage/{game_id}/{round}','ImageController@randomImage');
    Route::get('getCategories','ImageController@getCategories');
});

