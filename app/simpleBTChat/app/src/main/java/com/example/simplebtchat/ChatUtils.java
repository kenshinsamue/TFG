package com.example.simplebtchat;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.LinkPermission;
import java.util.UUID;


public class ChatUtils {
  private Context context;
  private final Handler handler;
  private BluetoothAdapter bluetoothAdapter;
  private ConnectThread connectThread;
  private AcceptThread acceptThread;
  private ConnectedThread connectedThread;

  private final UUID APP_UUID = UUID.fromString("fa87c0d0-afac-11de-8a39-0800200c9a66");
  private final String APP_NAME= "BluetoothChat";

  public static final int STATE_NONE = 0;
  public static final int STATE_LISTEN = 1;
  public static final int STATE_CONNECTING = 2;
  public static final int STATE_CONNECTED = 3;

  private int state ;

  public ChatUtils(Context context, Handler handler){
    this.context= context;
    this.handler= handler;
    state = STATE_NONE;
    bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
  }
  public int getState(){
    return state;
  }
//  Metodo que permite cambiar los estados de la comunicacion y enviarselo a la activity principal
  public synchronized void setState(int state){
    this.state = state;
    handler.obtainMessage( MainActivity.MESSAGE_STATE_CHANGED, state,-1).sendToTarget();
  }
  public synchronized void reset(){
    if(connectThread!= null){
      connectThread.cancel();
      connectThread = null;
    }
    if(acceptThread == null ){
      acceptThread = new AcceptThread();
      acceptThread.start();
    }
    if(connectedThread != null){
      connectedThread.cancel();
      connectedThread = null;
    }
  }
//  Inicializamos el proceso de comunicacion
  private synchronized void start(){
    reset();
    setState(STATE_LISTEN);
  }
// paramos el proceso de comunicacion
  public synchronized void stop(){
    reset();
    setState(STATE_NONE);
  }
//  Conectamos a un dispositivo
  public void connect (BluetoothDevice device){
//    si el dispositivo ya esta conectado cancelamos el thread que nos permita conectar
    if (state == STATE_CONNECTED){
      connectThread.cancel();
      connectThread = null;
    }
// Creamos una instancia de Thread para conectar al dispositivo e inicializamso
    connectThread = new ConnectThread(device);
    connectThread.start();

//  Cancelamos cualquier thread que mantenga una comunicacion
    if(connectedThread != null){
      connectedThread.cancel();
      connectedThread = null;
    }
    setState(STATE_CONNECTING);
  }
//Metodo para escribir al hilo de conexion
  public void write(byte[] buffer){
    ConnectedThread conThread;
    synchronized (this){
      if(state != STATE_CONNECTED){
        return;
      }
      conThread= connectedThread;
    }
    conThread.write(buffer);
  }

//  Mensaje que se encarga de actuar en caso de que la conexion se pierda
  private void connectionLost(){
//     Hacemos que la aplicacion tenga en cuenta de que la conexion se perdio
    sendMessageToMain("Connection Lost");
//    hacemos que, ya que se descarto la comunicacion, pueda empezar a escuchar a otro dispositivo
    ChatUtils.this.start();
  }
//  Metodo que permite enviar un mensaje al MainActivity
  private synchronized void sendMessageToMain(String mensaje){
    Message message = handler.obtainMessage(MainActivity.MESSAGE_TOAST);
    Bundle bundle = new Bundle();
    bundle.putString(MainActivity.TOAST,mensaje);
    message.setData(bundle);
    handler.sendMessage(message);
  }
// Si hay algun fallo en la comunicacion, al empezar
  private synchronized void connectionFailed(){
    sendMessageToMain("Cant connect to the device");
    ChatUtils.this.start();
  }
//Metodo para comunicar al MainActivity que actualmente el dispositivo esta conectado a otro
  private synchronized void connected(BluetoothSocket socket, BluetoothDevice device){
//     Cancelamos los hilos para conectar
    if(connectThread!=null){
      connectThread.cancel();
      connectThread = null;
    }
    if(connectedThread != null){
      connectedThread.cancel();
      connectedThread = null;
    }
//    Creamos un nuevo hilo de conexion pasandole un socket
    connectedThread = new ConnectedThread(socket);
    connectedThread.start();

//  Notificamos a main
    Message message = handler.obtainMessage(MainActivity.MESSAGE_DEVICE_NAME);
    Bundle bundle = new Bundle();
    bundle.putString(MainActivity.Device_NAME, device.getName());
    message.setData(bundle);
    handler.sendMessage(message);
    setState(STATE_CONNECTED);
  }
  private class AcceptThread extends Thread{
    private BluetoothServerSocket serverSocket;
//    Constructor Creamos un socket que escucha (servidor) y le especificamos que usara la version clasica de bluetooth (BR/EDR)
    public AcceptThread(){
      BluetoothServerSocket tmp = null;
      try{
        tmp = bluetoothAdapter.listenUsingRfcommWithServiceRecord(APP_NAME,APP_UUID);
      }catch (IOException e){
        Log.e("Accept->constructor", e.toString());
      }
      serverSocket = tmp;
    }
//
    public void run (){
//       Si identifica una comunicacion a travez de un socket lo acepta
      BluetoothSocket socket = null;
      try{
        socket = serverSocket.accept();
      }catch (IOException e){
        Log.e("Accept->run", e.toString());
        try{
          serverSocket.close();
        }catch (IOException e1){
          Log.e("Accept->close", e.toString());

        }
      }
//      En caso de que el socket exista
      if(socket!=null){
//        Si el dispositivo esta en estado de escucha o en el proceso de conexion creamos un thread de conexion con el socket local y el del dispositivo remoto
        switch (state){
          case STATE_LISTEN:
          case STATE_CONNECTING:
            connected(socket,socket.getRemoteDevice());
            break;
//        Si el estado del dispositivo es nulo o conectado lo que hacemos es cancelar el socket
          case STATE_NONE:
          case STATE_CONNECTED:
            try{
              socket.close();
            }catch (IOException e){
              Log.e("Accept->closesocket", e.toString());
            }
            break;
        }
      }
    }
    public void cancel (){
      try{
       serverSocket.close();
      }catch (IOException e){
        Log.e("Accept->CloseServerSocket", e.toString());
      }
    }
  }
  private class ConnectThread extends Thread{
    private final BluetoothSocket socket;
    private final BluetoothDevice device;
//  Constructor del Thread, recibimos un device
    public ConnectThread(BluetoothDevice device){
//  creamos un socket para el dispositivo remoto a travez de Bluetooth clasico (BD/EDR)
      this.device = device;
      BluetoothSocket tmp = null;
      try{
        tmp = device.createRfcommSocketToServiceRecord(APP_UUID);
      }catch (IOException e){
        Log.e("Connect->constructor", e.toString());
      }
      socket = tmp;
    }

    public void run (){
//  Intentamos conectar al socket del dispositivo remoto
      try{
        socket.connect();
      }catch (IOException e_){
        Log.e("Connect->Run", e_.toString());
        try{
          Log.d("La ejecucion del trhead ha sido interrumpida",", vamos a cerrar el socket");
          socket.close();
        }catch (IOException e){
          Log.e("Connect->CloseSocket", e.toString());
        }
        connectionFailed();
        return;
      }
      synchronized (ChatUtils.this){
        connectThread = null;
      }
//    Terminamos de conectar y notificamos al sistema de que estamos conectados
      connected(socket,device);
    }

    public void cancel(){
      try {
        socket.close();
      }catch (IOException e){
        Log.e("Connect->Cancel", e.toString());
      }
    }
  }
  private class ConnectedThread extends  Thread{

    private final BluetoothSocket socket;
    private final InputStream inputStream;
    private final OutputStream outputStream;

    public ConnectedThread(BluetoothSocket socket){
      this.socket = socket;
      InputStream tmpin = null;
      OutputStream tmpout = null;
      try{
        tmpin = socket.getInputStream();
        tmpout = socket.getOutputStream();
      }catch (IOException e){
      }
      inputStream= tmpin;
      outputStream = tmpout;
    }

    public void run(){
      byte [] buffer = new byte[1024];
      int bytes;
      while(true){
        try{
          bytes = inputStream.read(buffer);
          handler.obtainMessage(MainActivity.MESSAGE_READ,bytes,-1,buffer).sendToTarget();
        }catch (IOException e){
          connectionLost();
        }
      }
    }

    public void write(byte[] buffer){
      int tmp = state;
      try {
        outputStream.write(buffer);
        handler.obtainMessage(MainActivity.MESSAGE_WRITE,-1,-1,buffer).sendToTarget();
      }catch (IOException e){
        Log.e("Error al escribir",e.toString());
      }
    }

    public void cancel (){
      try{
        socket.close();
      }catch (IOException e){
        Log.e(" Error al cerrar  -> ",e.toString());
      }
    }
  }
}
