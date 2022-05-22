package com.example.simplebtchat;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothClass;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Handler;
import android.os.Message;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import java.nio.charset.StandardCharsets;

public class MainActivity extends AppCompatActivity {


  private Context context;
  private BluetoothAdapter bluetoothAdapter;
  private ChatUtils chatUtils;

  private ListView listMainchat;
  private EditText edCreateMessage;
  private Button btnSendMessage;
  private ArrayAdapter<String> adapterMainChat;

  private final int LOCATION_PERMISSION_REQUEST = 101;
  private final int SELECT_DEVICE = 102;

  public static final int MESSAGE_STATE_CHANGED = 0;
  public static final int MESSAGE_READ = 1;
  public static final int MESSAGE_WRITE = 2;
  public static final int MESSAGE_DEVICE_NAME = 3;
  public static final int MESSAGE_TOAST = 4;

  public static final String Device_NAME = "deviceName";
  public static final String TOAST = "toast";

  private String ConnectedDevice;
  //  Handler de las peticiones y mensajes que ChatUtils envia a esta activity
  private Handler handler = new Handler(new Handler.Callback() {
    @Override
    public boolean handleMessage(@NonNull Message message) {
      switch (message.what) {
//        si el estado ha cambiado habra que ver en que resuelve
        case MESSAGE_STATE_CHANGED:
          switch (message.arg1) {
            case ChatUtils.STATE_NONE:
            case ChatUtils.STATE_LISTEN:
              setState("Not Connected");
              break;
            case ChatUtils.STATE_CONNECTING:
              setState("Connecting ...");
              break;
            case ChatUtils.STATE_CONNECTED:
              setState("Connected: " + ConnectedDevice);
              break;
          }
          break;
//Si se requiere escribir el mensaje recogemos el buffer, lo enviamos y lo registramos en el chat
        case MESSAGE_WRITE:
          byte[] buffer1 = (byte[]) message.obj;
          String outputBuffer = new String(buffer1);
          adapterMainChat.add("Me: " + outputBuffer);
          break;
// Por otro lado si se desea leer lo que hacemos es registrar en el chat
        case MESSAGE_READ:
          byte[] buffer = (byte[]) message.obj;
          String inputBuffer = new String(buffer, 0, message.arg1);
          adapterMainChat.add(ConnectedDevice + ": " + inputBuffer);
          break;
// Si recibimos la informacion del nombre del dispositivo guardamos en la variable global
        case MESSAGE_DEVICE_NAME:
          ConnectedDevice = message.getData().getString(Device_NAME);
          Toast.makeText(context, ConnectedDevice, Toast.LENGTH_SHORT).show();
          break;
// Si necesitamos que se muestre un mensaje determinado en pantalla, como pop-up
        case MESSAGE_TOAST:
          Toast.makeText(context, message.getData().getString(TOAST), Toast.LENGTH_SHORT).show();
          break;
      }
      return false;
    }
  });

  private void setState(CharSequence subTitle) {
    getSupportActionBar().setSubtitle(subTitle);
  }

  //Al momento de crear la activity, guardamos el contexto e inicializamos todos los mecanismos del chat ademas de los presets de bluetooth
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);
    context = this;
    init();
    initBluetooth();
    chatUtils = new ChatUtils(context, handler);
  }

  //  Inicializamos los elementos del chat y creamos un Listener para cuando se envie un mensaje
  private void init() {
    listMainchat = findViewById(R.id.lista_conversacion);
    edCreateMessage = findViewById(R.id.mensaje_entrada);
    btnSendMessage = findViewById(R.id.btn_send_msg);

//  Adaptador para poder indrucir elementos a la lista de la conmversacion
    adapterMainChat = new ArrayAdapter<String>(context, R.layout.message_layout);
    listMainchat.setAdapter(adapterMainChat);

    btnSendMessage.setOnClickListener(new View.OnClickListener() {
      @Override
      public void onClick(View view) {
        String message = edCreateMessage.getText().toString();
        if (!message.isEmpty()) {
          edCreateMessage.setText("");
          chatUtils.write(message.getBytes());
        }
      }
    });
  }

  // Metodo inicia y guarda el adaptador bluetooth, si no hay deberia terminar la app
  private void initBluetooth() {
    bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    if (bluetoothAdapter == null) {
      Toast.makeText(context, "Not Bluetooth found", Toast.LENGTH_SHORT).show();
    }
  }

  //  Metodo que permite la creacion y la anexion del menu
  @Override
  public boolean onCreateOptionsMenu(Menu menu) {
    getMenuInflater().inflate(R.menu.menu_main_activity, menu);
    return super.onCreateOptionsMenu(menu);
  }

  // Metodo que permite decidir que hacer al clickar los botones del menu
  @Override
  public boolean onOptionsItemSelected(@NonNull MenuItem item) {
    switch (item.getItemId()) {
//      Verificamos que los permisos necesarios estan facilitados, si no los pedimos , en caso contrario vamos a la activity de la lista de dispositivos
      case R.id.menu_search_devices:
        checkPermissions();
        return true;
      case R.id.menu_enable_bt:
//        Habilitamos las propiedades del dispositivo para que este conectable y visible
        enableBluetooth();
        return true;
      default:
        return super.onContextItemSelected(item);
    }
  }

  //  verificamos los permisos y nos movemos a la activity de la lista de dispositivos
  private void checkPermissions() {
    if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
      ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, LOCATION_PERMISSION_REQUEST);
    } else {
      Intent intent = new Intent(context, DeviceListActivity.class);
      startActivityForResult(intent, SELECT_DEVICE);
    }
  }

  //  Este metodo define lo que haremos al momento de terminar el proceso de una actividad, se maneja entre los requestCode, y resultCode para decidir que hacer
  @Override
  protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
//     Si lo que queremos es seleccionar un dispositivo y el resultado devuelto es OK
    if (requestCode == SELECT_DEVICE && resultCode == RESULT_OK) {
//        Guardamos la direccion BTADDR y conectamos a esa direccion
      String address = data.getStringExtra("deviceAddress");
      chatUtils.connect(bluetoothAdapter.getRemoteDevice(address));
    }
    super.onActivityResult(requestCode, resultCode, data);
  }

  //Este metodo maneja el resultado al solicitar los permisos
  @Override
  public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
//    Si el permiso que se va a solicitar es Acceso al sistema de almacenaje
    if (requestCode == LOCATION_PERMISSION_REQUEST) {
//      Si nos dan el permiso para acceder, nos movemos a la activity de la lista de dispositivo
      if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
        Intent intent = new Intent(context, DeviceListActivity.class);
        startActivityForResult(intent, SELECT_DEVICE);
      }
//      En otro caso volvemos a preguntar, si nos da el permiso vamos a checkPermission(), en caso contrario cerramos la app
      else {
        new AlertDialog.Builder(context)
                .setCancelable(false)
                .setMessage("Location Permission is required.")
                .setPositiveButton("Grant", new DialogInterface.OnClickListener() {
                  @Override
                  public void onClick(DialogInterface dialogInterface, int i) {
                    checkPermissions();
                  }
                })
                .setNegativeButton("Deny", new DialogInterface.OnClickListener() {
                  @Override
                  public void onClick(DialogInterface dialogInterface, int i) {
                    MainActivity.this.finish();
                  }
                }).show();
      }
    }
    super.onRequestPermissionsResult(requestCode, permissions, grantResults);
  }

  //  Metodo apara habilitar el dispositivo y permitir que el dispositivo sea visible y que se puedan conectar
  private void enableBluetooth() {
    if (!bluetoothAdapter.isEnabled()) {

      bluetoothAdapter.enable();
    }

    if(bluetoothAdapter.getScanMode() != BluetoothAdapter.SCAN_MODE_CONNECTABLE_DISCOVERABLE){
      Intent discoveryIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE);
      discoveryIntent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION,300);
      startActivity(discoveryIntent);
    }
  }

  @Override
  protected void onDestroy() {
    super.onDestroy();
    if(chatUtils!=null){
      chatUtils.stop();
    }
  }
}