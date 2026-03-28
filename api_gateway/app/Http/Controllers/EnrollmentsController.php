<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class EnrollmentsController extends Controller
{
    public function create_enrollment(Request $request){
        $user = auth()->user();

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
        ])->post(env("ENROLLMENTS_ENDPOINT"),[
            "course_id" => $request->course_id,
            "user_id" => $user->id,
            "status" => $request->status,
        ]);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function index_enrollments(){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("ENROLLMENTS_ENDPOINT"));

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function index_enrollment($id){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->get(env("ENROLLMENTS_ENDPOINT").$id."/");

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }
    
    public function update_enrollment(Request $request, $id){

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
        ])->put(env("ENROLLMENTS_ENDPOINT").$id."/",[
            "course_id" => $request->course_id,
            "status" => $request->status,
        ]);

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }

    public function delete_enrollment($id){
        $response = Http::withHeaders([
            "Authorization" => env("SERVICES_TOKEN")
        ])->delete(env("ENROLLMENTS_ENDPOINT").$id."/");

        return [
            "status" => $response->status(),
            "body" => $response->json()
        ];
    }
}


