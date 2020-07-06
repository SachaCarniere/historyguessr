<?php

use Illuminate\Database\Seeder;

class DataTableSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        DB::table('data')->insert([
            'year' => 1998,
            'filePath' => app('url')->asset("game/1.jpg", false),
        ]);
    }
}
