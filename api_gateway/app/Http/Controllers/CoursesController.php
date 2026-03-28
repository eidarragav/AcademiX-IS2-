<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class CoursesController extends Controller
{
    public function create_course(Request $request){
        $instructor = auth()->user();

        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->post(env("COURSES_ENDPOINT"),[
            "title" => $request->title,
            "description" => $request->description,
            "category" => $request->category,
            "level" => $request->level,
            "instructor_id" => $instructor->id,
        ]);

        return [
            "status" => $response->status(),
            "body" => $response->body()
        ];
    }

    public function index_courses(){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("COURSES_ENDPOINT"));

        return [
            "status" => $response->status(),
            "body" => $response->body()
        ];
    }

    public function index_course($id){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("COURSES_ENDPOINT")."/".$id);

        return [
            "status" => $response->status(),
            "body" => $response->body()
        ];
    }

    public function update_course(Request $request, $id){

        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->put(env("COURSES_ENDPOINT")."/".$id,[
            "title" => $request->title,
            "description" => $request->description,
            "category" => $request->category,
            "level" => $request->level,
        ]);

        return [
            "status" => $response->status(),
            "body" => $response->body()
        ];
    }

    public function delete_course(Request $request, $id){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->delete(env("COURSES_ENDPOINT")."/".$id);

        return [
            "status" => $response->status(),
            "body" => $response->body()
        ];
    }
}
