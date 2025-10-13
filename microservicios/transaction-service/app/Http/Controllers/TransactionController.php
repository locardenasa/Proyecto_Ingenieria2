<?php

namespace App\Http\Controllers;

use App\Models\Transaction;
use Illuminate\Http\Request;

class TransactionController extends Controller
{
    // Listar todas las transacciones
    public function index()
    {
        $transactions = Transaction::all();
        return response()->json($transactions);
    }

    // Crear nueva transacción
    public function store(Request $request)
    {
        $transaction = Transaction::create($request->all());
        return response()->json($transaction, 201);
    }

    // Mostrar una transacción
    public function show($id)
    {
        $transaction = Transaction::find($id);
        
        if (!$transaction) {
            return response()->json(['error' => 'Transacción no encontrada'], 404);
        }

        return response()->json($transaction);
    }

    // Actualizar transacción
    public function update(Request $request, $id)
    {
        $transaction = Transaction::find($id);
        
        if (!$transaction) {
            return response()->json(['error' => 'Transacción no encontrada'], 404);
        }

        $transaction->update($request->all());
        return response()->json($transaction);
    }

    // Eliminar transacción
    public function destroy($id)
    {
        $transaction = Transaction::find($id);
        
        if (!$transaction) {
            return response()->json(['error' => 'Transacción no encontrada'], 404);
        }

        $transaction->delete();
        return response()->json(['message' => 'Transacción eliminada']);
    }
}