<?php
include_once('simple_html_dom.php');

function getStatusCodeMessage($status)
{
    $codes = Array(
        100 => 'Continue',
        101 => 'Switching Protocols',
        200 => 'OK',
        201 => 'Created',
        202 => 'Accepted',
        203 => 'Non-Authoritative Information',
        204 => 'No Content',
        205 => 'Reset Content',
        206 => 'Partial Content',
        300 => 'Multiple Choices',
        301 => 'Moved Permanently',
        302 => 'Found',
        303 => 'See Other',
        304 => 'Not Modified',
        305 => 'Use Proxy',
        306 => '(Unused)',
        307 => 'Temporary Redirect',
        400 => 'Bad Request',
        401 => 'Unauthorized',
        402 => 'Payment Required',
        403 => 'Forbidden',
        404 => 'Not Found',
        405 => 'Method Not Allowed',
        406 => 'Not Acceptable',
        407 => 'Proxy Authentication Required',
        408 => 'Request Timeout',
        409 => 'Conflict',
        410 => 'Gone',
        411 => 'Length Required',
        412 => 'Precondition Failed',
        413 => 'Request Entity Too Large',
        414 => 'Request-URI Too Long',
        415 => 'Unsupported Media Type',
        416 => 'Requested Range Not Satisfiable',
        417 => 'Expectation Failed',
        500 => 'Internal Server Error',
        501 => 'Not Implemented',
        502 => 'Bad Gateway',
        503 => 'Service Unavailable',
        504 => 'Gateway Timeout',
        505 => 'HTTP Version Not Supported'
    );

    return (isset($codes[$status])) ? $codes[$status] : '';
}

// Helper method to send a HTTP response code/message
function sendResponse($status = 200, $body = '', $content_type = 'text/html')
{
    $status_header = 'HTTP/1.1 ' . $status . ' ' . getStatusCodeMessage($status);
    header($status_header);
    header('Content-type: ' . $content_type);
    echo $body;
}

class ImecaAPI {

	function findMaxVal(array $array) {
		$maxVal = 0;
		$count = count($array);
		for ($i=0; $i<$count; $i++){
			$val = preg_replace('/[^0-9]/', '', $array[$i]);
			$maxVal = max($val,$maxVal);
		}
		return $maxVal;
	}
	
    function new_scrape() {
		$imecas;
		$hora;
		$fecha;
		$riesgos;

//         $url = 'http://148.243.232.113:8080/calidadaire/xml/simat.json';
        $url = 'http://104.236.189.141/imecas/';
//         $url = 'http://google.com';

         header('Content-type: application/json');
		$json = file_get_contents($url);
//         var_dump($json);
//         $error = error_get_last();
//         echo "HTTP request failed. Error was: " . $error['message'];

//         $ch = curl_init($url);
//         curl_setopt($ch, CURLOPT_URL, $url);
//         curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
//         curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
//         $content = curl_exec($ch);
//         var_dump($content);
//         curl_close($ch); 
//         echo $content;
/*
		$json = file_get_contents($url);
        var_dump($content);
        $error = error_get_last();
        echo "HTTP request failed. Error was: " . $error['message'];
*/

        $decoded = json_decode($json, true);
//         var_dump($decoded);
        $main_node = $decoded['pollutionMeasurements'];
        $fecha = $main_node['timeStamp'];
        $hora = $main_node['report'];
        $maxVal = 0;
        $maxPollutant;
        foreach ($main_node['delegations'] as $delegation) {
            if ($delegation['imecaPoints'] != 'N.D') {
                if ($delegation['imecaPoints'] > $maxVal) {
                    $maxVal = $delegation['imecaPoints'];
                    $maxPollutant = $delegation['pollutant'];
                }
            }
        }
        foreach ($main_node['stations'] as $station) {
            if ($station['imecaPoints'] != 'N.D') {
                if ($station['imecaPoints'] > $maxVal) {
                    $maxVal = $station['imecaPoints'];
                    $maxPollutant = $station['pollutant'];
                }
            }
        }
        return array($maxVal, $maxPollutant, $hora, $fecha);
	}

/*
	function scrape() {
		$imecas;
		$hora;
		$fecha;
		$riesgos;

		$html = file_get_html('http://148.243.232.113:8080/calidadaire/calidadaire/reporteimeca.php');
//		$html = file_get_html('http://www.calidadaire.df.gob.mx/calidadaire/reporteimeca.php');
		$fecha_node = $html->find('div[id=fecha]');
		$hora_node = $html->find('div[id=hora]');
		$imeca_node = $html->find('div[id=imeca]');
		$valores_zona = $html->find('table.tablavaloresimecazona tr');
		
		$maxContaminante;
		$maxVal = 0;
		for($i=1;$i<6;$i++){
			$values = $valores_zona[$i]->find('td.contenidostablavaloresimecazona');
			$contaminante = strip_tags($values[0]);
			$val2 = $this->findMaxVal(array_slice($values,1));
			if ($val2 > $maxVal) {
				$maxVal = $val2;
				$maxContaminante = $contaminante;
			}
		}
		$fecha = strip_tags($fecha_node[0]);
		$hora = preg_replace('/[^0-9]/', '', $hora_node[0]);
		preg_match('/\((.*?)\)/', $maxContaminante, $maxContaminante);
		return array($maxVal, $maxContaminante, $hora, $fecha);
	}
*/
	function passthrough() {
        $url = 'http://104.236.189.141/imecas/';
        sendResponse(200, file_get_contents($url));
	}
	
    function consulta_imeca() {
        $imecas;
        $particula;
        $hora;
        $fecha;
        $minuto;
        //$consulta = array();
        $handle = fopen("ultimoreporte.txt", "r");
        if ($handle) {
            while (($line = fgets($handle)) !== false) {
                // [0] key, [1] val
                $values = preg_split('/:/', $line);
                $key = trim($values[0]);
                $val = trim($values[1]);
                if ($key == "imecas") {
                    $imecas = $val;
                } else if ($key == "particula") {
                    $particula = $val;
                } else if ($key == "hora") {
                    $hora = $val;
                } else if ($key == "minuto") {
                    $minuto = $val;
                } else if ($key == "fecha") {
                    $fecha = $val;
                }
            }
        } else {
            // error opening the file.
        } 
        fclose($handle);

        $current_hour = date("H");
        $curr_date = date("Y-m-d");
        $update = false;
        if ($curr_date > $fecha) {
            $update = true;
        }
        else if ($current_hour > $hora) {
            $update = true;
        }
        else if ($hora == 24) {
            $update = true;
        }
        $scrape = $this->new_scrape();
        if ($update == true) {
            $curr_min = date("i");
            //$minuto = $consulta[minuto];
            // dejamos pasar al menos un minuto antes de reintentar
            if (true) {
                $scrape = $this->new_scrape();
                $imecas = $scrape[0];
                $particula = $scrape[1];
                $hora = $scrape[2];
                $fecha = $scrape[3];
                // Guarda la nueva informacion
                $file = fopen("ultimoreporte.txt", "w");
                if ($file) {
                    fwrite($file, "imecas:$imecas\r\n");
                    fwrite($file, "particula:$particula\r\n");
                    fwrite($file, "fecha:$fecha\r\n");
                    fwrite($file, "hora:$hora\r\n");
                    if ($hora >= $current_hour) {
                    // Si ya es el reporte nuevo, resetea el minuto a 0
                        fwrite($file, "minuto:0\r\n");
                    } else {
                        fwrite($file, "minuto:$curr_min\r\n");                    
                    }
                } else {
                    // error opening the file.
                } 
                fclose($file);
            }
            else {
                $file = fopen("ultimoreporte.txt", "w");
                if ($file) {
                    fwrite($file, "imecas:$imecas\r\n");
                    fwrite($file, "particula:$particula\r\n");
                    fwrite($file, "hora:$hora\r\n");
                    fwrite($file, "fecha:$fecha\r\n");
                    fwrite($file, "minuto:$minuto\r\n");
                } else {
                    // error opening the file.
                }
                fclose($file);
            }
        }
        $consulta = array(
            "imecas" => $imecas,
            "particula" => $particula,
            "hora"	=> $hora,
            "fecha"=> $fecha,
        );
        sendResponse(200, json_encode($consulta));
        return true;
    }

}

$api = new ImecaAPI;
$api-> passthrough();
// $api-> new_scrape();

?>