<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class LessonsController extends Controller
{
    public function index_lesson($id){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("CONTENT_LESSONS_ENDPOINT")."/".$id);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function index_lessons(){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("CONTENT_LESSONS_ENDPOINT"));

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function create_lesson(Request $request){

    }

    public function update_lesson(Request $request, $id){

    } 
    
    public function delete_lesson($id){

    }
}
