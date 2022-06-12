#!/bin/bash


POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -l|--lap)
      LAP="$2"
      shift 
      shift
      ;;
    -u|--UAP)
      UAP="$2"
      shift 
      shift 
      ;;
    -r|--register)
      LOG="$2"
      shift
      shift
      ;;
    -f|--filename)
      FILENAME="$2"
      shift
      shift
      ;;
    -t)
      TIME="$2" 
      shift 
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



ubertooth-rx -q ${FILENAME} -l ${LAP} -u ${UAP} -t ${TIME} > ${LOG}