# Clase que representa un proceso en el sistema.
class Process:
    def __init__(self, name, burst_time, arrival_time, queue, priority):
        # Inicializa los atributos del proceso.
        self.name = name  # Nombre del proceso
        self.burst_time = burst_time  # Tiempo de ejecución requerido por el proceso
        self.remaining_time = burst_time  # Tiempo restante para completar el proceso
        self.arrival_time = arrival_time  # Tiempo de llegada del proceso al sistema
        self.queue = queue  # Cola a la que pertenece el proceso
        self.priority = priority  # Prioridad del proceso
        self.completion_time = 0  # Tiempo de finalización del proceso
        self.waiting_time = 0  # Tiempo de espera del proceso
        self.turnaround_time = 0  # Tiempo de retorno del proceso
        self.response_time = 0  # Tiempo de respuesta del proceso

    # Método para representar el proceso como una cadena de texto.
    def __str__(self):
        return f"{self.name}(BT={self.burst_time}, AT={self.arrival_time}, Pr={self.priority})"


# Clase que representa el planificador de colas múltiples (MLQ).
class MLQScheduler:
    def __init__(self):
        # Inicializa las colas de procesos.
        self.queues = {1: [], 2: [], 3: []}  # Tres colas (1, 2 y 3)
        self.current_time = 0  # Tiempo actual del sistema
        self.execution_order = []  # Lista para almacenar el orden de ejecución de los procesos

    # Método para agregar un proceso a la cola correspondiente.
    def add_process(self, process):
        self.queues[process.queue].append(process)  # Añade el proceso a la cola especificada

    # Método para planificar los procesos en la cola utilizando el algoritmo First-Come, First-Served (FCFS).
    def schedule_fcfs(self, queue):
        for process in queue:  # Itera sobre los procesos en la cola
            # Si el tiempo actual es menor que el tiempo de llegada del proceso, se adelanta al tiempo de llegada.
            if self.current_time < process.arrival_time:
                self.current_time = process.arrival_time
            self.current_time += process.burst_time  # Incrementa el tiempo actual por el tiempo de ejecución del proceso
            process.completion_time = self.current_time  # Establece el tiempo de finalización del proceso
            self.execution_order.append(process)  # Agrega el proceso al orden de ejecución
            process.turnaround_time = process.completion_time - process.arrival_time  # Calcula el tiempo de retorno
            process.waiting_time = process.turnaround_time - process.burst_time  # Calcula el tiempo de espera
            process.response_time = process.waiting_time  # En FCFS, tiempo de respuesta es igual al tiempo de espera

    # Método para planificar los procesos en la cola utilizando el algoritmo Round Robin (RR).
    def schedule_rr(self, time_quantum, queue):
        while queue:  # Mientras haya procesos en la cola
            process = queue.pop(0)  # Toma el primer proceso de la cola
            # Si el tiempo restante del proceso es mayor que el tiempo cuántico.
            if process.remaining_time > time_quantum:
                # Si el tiempo actual es menor que el tiempo de llegada, se adelanta al tiempo de llegada.
                if self.current_time < process.arrival_time:
                    self.current_time = process.arrival_time
                self.current_time += time_quantum  # Incrementa el tiempo actual por el tiempo cuántico
                process.remaining_time -= time_quantum  # Reduce el tiempo restante del proceso
                queue.append(process)  # Reagrega el proceso al final de la cola
            else:
                # Si el tiempo restante es menor o igual al tiempo cuántico, se completa el proceso.
                if self.current_time < process.arrival_time:
                    self.current_time = process.arrival_time
                self.current_time += process.remaining_time  # Incrementa el tiempo actual por el tiempo restante
                process.completion_time = self.current_time  # Establece el tiempo de finalización
                process.remaining_time = 0  # Marca el proceso como completado
                self.execution_order.append(process)  # Agrega el proceso al orden de ejecución
                process.turnaround_time = process.completion_time - process.arrival_time  # Calcula el tiempo de retorno
                process.waiting_time = process.turnaround_time - process.burst_time  # Calcula el tiempo de espera
                process.response_time = process.waiting_time  # Tiempo de respuesta igual al tiempo de espera

    # Método para planificar los procesos en la cola utilizando el algoritmo Shortest Job First (SJF).
    def schedule_sjf(self, queue):
        queue.sort(key=lambda p: p.burst_time)  # Ordena la cola según el tiempo de ejecución (burst time)
        for process in queue:  # Itera sobre los procesos en la cola
            if self.current_time < process.arrival_time:  # Si el tiempo actual es menor que el tiempo de llegada
                self.current_time = process.arrival_time  # Adelanta al tiempo de llegada
            self.current_time += process.burst_time  # Incrementa el tiempo actual por el tiempo de ejecución
            process.completion_time = self.current_time  # Establece el tiempo de finalización
            self.execution_order.append(process)  # Agrega el proceso al orden de ejecución
            process.turnaround_time = process.completion_time - process.arrival_time  # Calcula el tiempo de retorno
            process.waiting_time = process.turnaround_time - process.burst_time  # Calcula el tiempo de espera
            process.response_time = process.waiting_time  # Tiempo de respuesta igual al tiempo de espera

    # Método principal para ejecutar el planificador de colas múltiples.
    def run(self):
        for q in self.queues:  # Itera sobre las colas disponibles
            if self.queues[q]:  # Si hay procesos en la cola
                if q == 1:  # Si es la cola 1
                    self.schedule_fcfs(self.queues[q])  # Llama al planificador FCFS
                elif q == 2:  # Si es la cola 2
                    self.schedule_rr(3, self.queues[q])  # Llama al planificador RR con un tiempo cuántico de 3
                elif q == 3:  # Si es la cola 3
                    self.schedule_sjf(self.queues[q])  # Llama al planificador SJF

    # Método para calcular y devolver métricas de tiempo promedio de los procesos.
    def print_metrics(self):
        total_waiting_time = 0  # Inicializa el tiempo total de espera
        total_turnaround_time = 0  # Inicializa el tiempo total de retorno
        total_response_time = 0  # Inicializa el tiempo total de respuesta
        for process in self.execution_order:  # Itera sobre el orden de ejecución
            total_waiting_time += process.waiting_time  # Suma el tiempo de espera
            total_turnaround_time += process.turnaround_time  # Suma el tiempo de retorno
            total_response_time += process.response_time  # Suma el tiempo de respuesta

        num_processes = len(self.execution_order)  # Número total de procesos
        # Calcula el tiempo promedio de espera, retorno y respuesta
        avg_waiting_time = total_waiting_time / num_processes if num_processes else 0
        avg_turnaround_time = total_turnaround_time / num_processes if num_processes else 0
        avg_response_time = total_response_time / num_processes if num_processes else 0

        return avg_waiting_time, avg_turnaround_time, avg_response_time  # Devuelve las métricas calculadas


# Función para leer los procesos desde un archivo.
def read_processes_from_file(file_path):
    processes = []  # Lista para almacenar los procesos
    with open(file_path, 'r') as file:  # Abre el archivo
        for line in file:  # Itera sobre cada línea del archivo
            if line.startswith("#") or not line.strip():  # Ignora líneas de comentarios y vacías
                continue
            # Descompone la línea en los atributos del proceso
            name, burst_time, arrival_time, queue, priority = line.strip().split(';')
            # Crea un objeto Proceso y lo añade a la lista
            process = Process(name, int(burst_time), int(arrival_time), int(queue), int(priority))
            processes.append(process)  # Añade el proceso a la lista
    return processes  # Devuelve la lista de procesos


# Función para escribir métricas y resultados en un archivo.
def write_metrics_to_file(file_path, processes, metrics):
    with open(file_path, 'w') as file:  # Abre el archivo para escritura
        file.write("# archivo: output_mlq.txt\n")  # Escribe la cabecera
        file.write("# etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT\n")  # Escribe la cabecera de métricas
        for p in processes:  # Itera sobre cada proceso
            # Escribe las métricas del proceso en el archivo
            file.write(f"{p.name};{p.burst_time};{p.arrival_time};{p.queue};{p.priority};{p.waiting_time};{p.completion_time};{p.response_time};{p.turnaround_time}\n")
        # Escribe las métricas promedio calculadas
        file.write(f"WT={metrics[0]}; CT={metrics[1]}; RT={metrics[2]}; TAT={metrics[1] + metrics[0] / len(processes)};\n")


# Función principal que ejecuta el planificador de procesos.
def main():
    file_path = 'mlq025.txt'  # Ruta del archivo de entrada
    processes = read_processes_from_file(file_path)  # Lee los procesos desde el archivo

    scheduler = MLQScheduler()  # Crea una instancia del planificador MLQ
    for process in processes:  # Itera sobre cada proceso
        scheduler.add_process(process)  # Añade el proceso al planificador

    scheduler.run()  # Ejecuta el planificador
    metrics = scheduler.print_metrics()  # Obtiene las métricas promedio
    output_file_path = 'output_mlq.txt'  # Ruta del archivo de salida
    write_metrics_to_file(output_file_path, scheduler.execution_order, metrics)  # Escribe las métricas en el archivo

# Punto de entrada del programa.
if __name__ == "__main__":
    main()  # Llama a la función principal
