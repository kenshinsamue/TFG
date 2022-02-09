#!/bin/bash


POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -l|--lap)
      LAP="$2"
      shift # past argument
      shift # past value
      ;;
    -u|--UAP)
      UAP="$2"
      shift # past argument
      shift # past value
      ;;
    -r|--register)
      LOG="$2"
      shift # past argument
      shift
      ;;
    -f|--filename)
      FILENAME="$2"
      shift
      shift
      ;;
    -t)
      TIME="$2" # save positional arg
      shift # past argument
      shift
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

echo "LAP  = ${LAP}"
echo "UAP  = ${UAP}"
echo "LOGFILE   = ${LOG}"
echo "PCAP FILE = ${FILENAME}"
echo "TIME = ${TIME}"



# ubertooth-rx -q informacion.pcap -l df039f -u 49 -t 60 > registros.log