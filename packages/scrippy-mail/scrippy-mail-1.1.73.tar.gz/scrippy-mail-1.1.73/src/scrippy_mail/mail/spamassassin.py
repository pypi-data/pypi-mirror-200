"""Le module scrippy_mail.mail.SpamAssassin est une implémentation basique de Spamassassin."""
import time
import socket
import logging
from io import BytesIO
from scrippy_mail import ScrippyMailError


class SpamAssassinClient:
  """
  Implémentaton d'une partie du protocole SpamAssassin.

  https://svn.apache.org/repos/asf/spamassassin/trunk/spamd/PROTOCOL
  Par défaut le serveur SpamAssassin utilisé est la machine locale '127.0.0.1'.
  """

  def __init__(self, host='127.0.0.1', port=783, timeout=2):
    """Initialise le client."""
    self.host = host
    self.port = port
    self.timeout = timeout
    self.socket = None

  def __enter__(self):
    """Point d'entrée."""
    self.connect()
    return self

  def __exit__(self, type_err, value, traceback):
    """Point de sortie."""
    del type_err, value, traceback
    self.close()

  def connect(self):
    """Se connecte au serveur SpamAssassin défini au moment de l'instanciation."""
    logging.debug("[+] Connecting to SpamAssassin server")
    logging.debug(f" '-> {self.host}:{self.port}")
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.settimeout(self.timeout)
    self.socket.connect((self.host, self.port))

  def close(self):
    """Ferme la connexion au serveur SpamAssassin."""
    logging.debug("[+] Closing connection to SpamAssassin")
    self.socket.shutdown(socket.SHUT_WR)
    self.socket.close()

  def _send_data(self, data):
    """Envoie un message (au sens protocole d'échange SpamaAssassin) au serveur SpamaAssassin.

    Cette méthode est utilisée par toutes les méthodes ayant besoin de communiquer avec le serveur SpamAssassin.
    https://svn.apache.org/repos/asf/spamassassin/trunk/spamd/PROTOCOL
    """
    try:
      self.socket.sendall(data)
      logging.debug(f"Sent: {data}")
    except Exception as err:
      err_msg = f"Error while communicating with SpamAssassin server: [{err.__class__.__name__}]: {err}"
      logging.error(err_msg)
      raise ScrippyMailError(err_msg) from err

  def _recv_data(self, bufsize=8192):
    data = b''
    start = time.time()
    while time.time() - start < self.timeout:
      try:
        packet = self.socket.recv(bufsize)
        data += packet
      except Exception as err:
        logging.debug(f"{time.time() - start}/{self.timeout}")
        logging.debug(f"[{err.__class__.__name__}]: {err}")
    logging.debug(f"Received: {data}")
    return data

  def learn(self, mail, mail_type):
    """
    Donne au serveur SpamAssassin le courriel à apprendre.
    https://svn.apache.org/repos/asf/spamassassin/trunk/spamd/PROTOCOL
    """
    logging.debug(f"[+] Saving email as [{mail_type.upper()}]")
    try:
      buffer = BytesIO()
      buffer.write(b'TELL SPAMC/1.3\r\n')
      buffer.write(b'Content-Length: %d\r\n' % len(mail))
      buffer.write(b'Message-class: %s\r\n' % mail_type.encode())
      buffer.write(b'Set: local, remote\r\n\r\n')
      buffer.write(mail.encode())
      logging.debug(str(buffer.getvalue()))
      self._send_data(buffer.getvalue())
      # On a besoin de récupérer les données même si on ne s'en sert pas
      resp = self._recv_data()
    except Exception as err:
      err_msg = f"Error while learning: [{err.__class__.__name__}]: {err}"
      logging.error(err_msg)
      raise ScrippyMailError(err_msg) from err

  def check_spam(self, mail):
    """
    Vérifie le courriel passé en argument.

    Renvoie True sie le courriel est considéré comme un spam et fasle dans le cas contraire.
    Le résultat et le score sont inscrits dans le log de debug.
    """
    logging.debug("[+] Checking if email is spam")
    results = {"True": True, "False": False}
    try:
      buffer = BytesIO()
      buffer.write(b'TELL SPAMC/1.3\r\n')
      buffer.write(b'Content-Length: %d\r\n\r\n' % len(mail))
      buffer.write(mail.encode())
      logging.debug(str(buffer.getvalue()))
      self._send_data(buffer.getvalue())
      data = self._recv_data().split("\r\n")
      if data[0].split()[3] == b'OK':
        result = data[1].split()
        score = f"{result[3].decode().strip()}/{result[5].decode().strip()}"
        result = results[result[1].decode().strip()]
        logging.debug(f"Result: {result} | Score: {score}")
        return result
      # Si on arrive ici, c'est qu'une erreur est survenue
      # On renvoie l'exception pour qu'elle soit attrapée plus bas.
      # Touche pas à ça p'tit con©
      raise Exception(f"{data}")
    except Exception as err:
      err_msg = f"Error while checking for spam level: [{err.__class__.__name__}]: {err}"
      logging.error(err_msg)
      raise ScrippyMailError(err_msg) from err
