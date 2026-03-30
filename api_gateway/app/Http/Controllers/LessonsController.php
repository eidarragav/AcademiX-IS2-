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
        $module_exist = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("CONTENT_MODULES_ENDPOINT")."/".$request->course_id);

        if($course_exist->status() == 404){
            return [
                "mensaje" => "el modulo no existe"
            ];
        };


        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->post(env("CONTENT_LESSONS_ENDPOINT"),[
            "module_id" => $request->module_id,
            "title" => $request->title,
            "type" => $request->type,
            "content" => $request->content
        ]);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function update_lesson(Request $request, $id){

    } 
    
    public function delete_lesson($id){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->delete(env("CONTENT_LESSONS_ENDPOINT")."/".$id);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }
}
