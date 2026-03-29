<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class ModulesController extends Controller
{
    public function create_module(Request $request){

        $course_exist = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("COURSES_ENDPOINT")."/".$request->course_id);

        if($course_exist->status() == 404){
            return [
                "mensaje" => "el curso no existe"
            ];
        };

        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->post(env("CONTENT_MODULES_ENDPOINT"),[
            "course_id" => $request->course_id,
            "title" => $request->title,
            "description" => $request->description
        ]);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function index_modules(){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("CONTENT_MODULES_ENDPOINT"));

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function index_module($id){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("CONTENT_MODULES_ENDPOINT")."/".$id);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function update_module(Request $request, $id){
        $course_exist = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("COURSES_ENDPOINT")."/".$request->course_id);

        if($course_exist->status() == 404){
            return [
                "mensaje" => "el curso no existe"
            ];
        };

        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->put(env("CONTENT_MODULES_ENDPOINT")."/".$id,[
            "course_id" => $request->course_id,
            "title" => $request->title,
            "description" => $request->description
        ]);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function delete_module($id){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->delete(env("CONTENT_MODULES_ENDPOINT")."/".$id);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }
}
