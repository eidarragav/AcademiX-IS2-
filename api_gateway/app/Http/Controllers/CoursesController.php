<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class CoursesController extends Controller
{
    public function create_course(Request $request){
        $instructor = auth()->user();

        $response = Http::withHeaders([
            "Authorization" => env("services_token")
        ])->post(env("courses_endpoint"),[
            "title" => $request->title,
            "description" => $request->description,
            "category" => $request->category,
            "level" => $request->level,
            "instructor_id" => $instructor->id,
        ]);

        return [
            "status" => $response->status,
            "body" => $response->body
        ];
    }

    public function index_courses(){
        $response = Http::withHeaders([
            "Authorization" => env("services_token")
        ])->get(env("courses_endpoint"));

        return [
            "status" => $response->status,
            "body" => $response->body
        ];
    }

    public function index_course($id){
        $response = Http::withHeaders([
            "Authorization" => env("services_token")
        ])->get(env("courses_endpoint")."/".$id);

        return [
            "status" => $response->status,
            "body" => $response->body
        ];
    }

    public function update_course(Request $request, $id){
        $instructor = auth()->user();

        $response = Http::withHeaders([
            "Authorization" => env("services_token")
        ])->put(env("courses_endpoint"."/".$id),[
            "title" => $request->title,
            "description" => $request->description,
            "category" => $request->category,
            "level" => $request->level,
        ]);

        return [
            "status" => $response->status,
            "body" => $response->body
        ];
    }

    public function delete_course(Request $request, $id){

    }
}
