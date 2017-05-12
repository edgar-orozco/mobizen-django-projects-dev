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
	
    function consulta_imeca() {
    	$consulta = $this->scrape();
        $result = array(
           "imecas" => $consulta[0],
           "particula" => $consulta[1][1],
           "hora"	=> $consulta[2],
           "fecha"=> $consulta[3],
        );
        sendResponse(200, json_encode($result));
        return true;
    }

}

$api = new ImecaAPI;
$api-> consulta_imeca();

?>