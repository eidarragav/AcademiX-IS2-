<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;

class AuthController extends Controller
{
    public function index()
    {
        $users = User::all();
        return response()->json($users);
    }


    public function register(Request $request)
    {
        $user = new User();
        $user->name = $request->name;
        $user->email = $request->email;
        $user->password = $request->password;
        $user->question = $request->question;
        $user->answer = $request->answer;
        $user->save();

        return response()->json("Usuario creado");
    }

    public function login(Request $request)
    {
        $user = User::where('email', $request->email)->first();

        if(!$user || !password_verify($request->password, $user->password)){
            return response()->json(['Acceso denegado' => 'Credenciales invalidades']);
        }

        $token = $user->createToken('auth_token')->plainTextToken;

        return response()->json([
            'access_token' => $token,
            'token_type' => 'Bearer'
        ]);
    }

    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete();
        return response()->json(["Message" => 'Logged out']);
    }

    public function restore_password(Request $request)
    {
        $user = User::where('email', $request->email)->first();

        if(!$user || $user->answer != $request->answer){
            return response()->json(["message" => "Respues incorrecta"]);
        }

        $user->password = $request->password;
        $user->save();

        return response()->json(["message" => "Contraseña actualizada"]);
    }
}