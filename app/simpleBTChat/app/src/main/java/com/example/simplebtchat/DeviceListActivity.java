package com.example.simplebtchat;
//https://www.youtube.com/watch?v=T2io34enYqk
import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Set;

public class DeviceListActivity extends AppCompatActivity {
  private ListView listpairedDevices, listAvaibleDevices;
  private ProgressBar progresScannDevices;

  private ArrayAdapter<String> adapterPairedDevices, adapterAvaibleDevices;
  private Context context;
  private BluetoothAdapter bluetoothAdapter;

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_device_list);
    context = this;
    init();
  }

//Este Metodo se dedica
  private void init (){
//    Nos traemos las Views de los dispositivos paired y los disponibles
    listpairedDevices = findViewById(R.id.list_paired_devices);
    listAvaibleDevices = findViewById(R.id.list_avaible_devices);
    progresScannDevices = findViewById(R.id.progress_scann_devices);

    adapterPairedDevices = new ArrayAdapter<String>(context,R.layout.device_list_item);
    adapterAvaibleDevices = new ArrayAdapter<String>(context,R.layout.device_list_item);

    listpairedDevices.setAdapter(adapterPairedDevices);
    listAvaibleDevices.setAdapter(adapterAvaibleDevices);
//  Creamos un Listener para la lista de dispositivos disponibles de modo que al clickar iniciamos el chat con ese dispositivo
    listAvaibleDevices.setOnItemClickListener(new AdapterView.OnItemClickListener() {
      @Override
      public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
        String info = ((TextView)view).getText().toString();
        String address = info.substring(info.length() - 17);
        Intent intent = new Intent();
        intent.putExtra("deviceAddress",address);
        setResult(RESULT_OK,intent);
        finish();
      }
    });

    bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    Set<BluetoothDevice> pairedDevices = bluetoothAdapter.getBondedDevices();

    if(pairedDevices != null && pairedDevices.size() > 0){
      for(BluetoothDevice device : pairedDevices){
        adapterPairedDevices.add(device.getName() + "\n"+device.getAddress());
      }
    }

    IntentFilter intentFilter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
    registerReceiver(bluetootDeviceListener,intentFilter);

    IntentFilter intentFilter1 = new IntentFilter(BluetoothAdapter.ACTION_DISCOVERY_FINISHED);
    registerReceiver(bluetootDeviceListener,intentFilter1);
// Litener para los dispositivos que ya estan emparejados , al seleccionarlos empieza el chat
    listpairedDevices.setOnItemClickListener(new AdapterView.OnItemClickListener() {
      @Override
      public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
        bluetoothAdapter.cancelDiscovery();

        String info = ((TextView) view).getText().toString();
        String address = info.substring(info.length() - 17);
        Log.d("Address",address);

        Intent intent = new Intent();
        intent.putExtra("deviceAddress",address);

        setResult(Activity.RESULT_OK,intent);
        finish();
      }
    });
  }
//  Metodo de Receptor de comunicaciones broadcast
  private BroadcastReceiver bluetootDeviceListener = new BroadcastReceiver() {
    @Override
    public void onReceive(Context context, Intent intent) {
      String action = intent.getAction();
      if(BluetoothDevice.ACTION_FOUND.equals(action)){
        BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
        if(device.getBondState()!= BluetoothDevice.BOND_BONDED){
          adapterAvaibleDevices.add(device.getName()+"\n"+device.getAddress());
        }
      }
      else if (BluetoothAdapter.ACTION_DISCOVERY_FINISHED.equals(action)) {
        progresScannDevices.setVisibility(View.GONE);
        if(adapterAvaibleDevices.getCount()==0){
          Toast.makeText(context," No new Devices found",Toast.LENGTH_SHORT).show();
        }
        else{
          Toast.makeText(context," click on the device to start the chat", Toast.LENGTH_SHORT).show();
        }
      }
    }
  };
//  Incluimos el menu en la actividad
  @Override
  public boolean onCreateOptionsMenu(Menu menu) {
    getMenuInflater().inflate(R.menu.menu_device_list,menu);
    return super.onCreateOptionsMenu(menu);
  }
//  Verificar que hacer cuando seleccionas algunos de los elementos del menu
  @Override
  public boolean onOptionsItemSelected(@NonNull MenuItem item) {
    switch (item.getItemId()){
      case R.id.menu_scan:
        scannDevices();
        return true;
      default:
        return super.onOptionsItemSelected(item);
    }
  }

//  Metodo que permite hacer Buscar dispositivos sercanos
  private void scannDevices(){
    progresScannDevices.setVisibility(View.VISIBLE);
    adapterAvaibleDevices.clear();
    Toast.makeText(context," Scan Started",Toast.LENGTH_SHORT).show();

    if(bluetoothAdapter.isDiscovering()){
      bluetoothAdapter.cancelDiscovery();
    }
    bluetoothAdapter.startDiscovery();
  }

  @Override
  protected void onDestroy() {
    super.onDestroy();
    if(bluetootDeviceListener != null){
      unregisterReceiver(bluetootDeviceListener);
    }
  }
}